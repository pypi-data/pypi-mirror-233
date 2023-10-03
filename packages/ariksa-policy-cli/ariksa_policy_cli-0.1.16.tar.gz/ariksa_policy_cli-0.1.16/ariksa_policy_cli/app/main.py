import typer
from ariksa_policy_cli.app.modules.utils.send_request import SendRequest
from ariksa_policy_cli.app.schemas.resource import HTTPMethods, APIResources, WorkflowStatus, WorkflowType
import asyncio
from loguru import logger
import time
from beautifultable import BeautifulTable

app = typer.Typer()


async def _is_snapshot_complete(snapshot_id: str, shared_secret, account_id: str) -> bool:
    logger.info("Waiting for processing to complete")
    s_req = SendRequest(shared_secret=shared_secret)
    is_complete = False
    while not is_complete:
        latest_workflow = await s_req.send_request(
            method=HTTPMethods.GET,
            resource=APIResources.WORKFLOWS.value,
            response_model=dict,
            workflow_type=WorkflowType.snapshot_processing.value,
            account_id=account_id,
            size=2,
        )
        if latest_workflow.get('items'):
            latest_snapshot = latest_workflow.get('items')[0].get('identifier')
            status = latest_workflow.get('items')[0].get('status')
            if status == WorkflowStatus.success.value and latest_snapshot == snapshot_id:
                logger.info("Processing Successfull. Fetching report")
                return latest_snapshot
        logger.info("Processing not completing. Will retry in 30s")
        time.sleep(30)
        pass

async def print_report(account_id, shared_secret):
    s_req = SendRequest(shared_secret=shared_secret)
    report = await s_req.send_request(
        method=HTTPMethods.GET,
        resource=APIResources.REPORT.value,
        response_model=list[dict],
        account_id=account_id,
        random='123'
    )
    table = BeautifulTable()
    table.columns.header = ['resource_id', 'rule', 'description', 'severity']
    for rec in report:
        if rec.get('config_id') == 'IAM-USER-PASSWORD-INACTIVE':
            continue
        table.rows.append([rec.get('cloud_resource_id'), rec.get('config_id'), rec.get('compliance_description'), rec.get('severity')])
    if len(report):
        logger.error("Following issues were seen after scanning inventory")
        print(table)
        return 0
    else:
        logger.info("No policy violation were onserved in repository")
        return 1


@app.command()
def trigger_discovery(branch: str, account_id:str, shared_secret: str):
    s_req = SendRequest(shared_secret=shared_secret)
    # Trigger gitlab acount rediscovery
    latest_snapshot = asyncio.run(s_req.send_request(
        method=HTTPMethods.GET,
        resource=APIResources.START_DISCOVERY.value,
        response_model=str,
        branch=branch,
        uuid=account_id

    ))
    logger.debug("Snapshot ID {}".format(latest_snapshot))
    # wait until snapshot is successfull
    asyncio.run(_is_snapshot_complete(snapshot_id=latest_snapshot, shared_secret=shared_secret,account_id=account_id))

    # Download report
    return asyncio.run(print_report(account_id=account_id, shared_secret=shared_secret))
