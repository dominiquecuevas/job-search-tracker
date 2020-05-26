import React from "react"
import moment from "moment"
import ApplicationsStatusChange from "./ApplicationsStatusChange"

function Applications(props) {
    return (
        <div>
            {props.applications.map(
                application => (
                    <details key={application.application_id}>
                        <summary>{application.job.title} - {application.job.company.company_name}</summary>
                        <p>Applied: {moment(application.datetime_applied).format("MM-DD-YYYY")}</p>
                        Current Status: <ApplicationsStatusChange 
                            new_status={application.application_statuses[0].status} 
                            application_id={application.application_id}
                            fetchUser={props.fetchUser}/>
                        <details>
                            <summary>Status History</summary>
                            {application.application_statuses.map((application_status) => 
                                <p key={application_status.application_status_id}>
                                    {moment(application_status.datetime_created).format("MM-DD-YYYY")}
                                    &nbsp;
                                    {application_status.status}
                                </p>
                            )}
                        </details>
                        <p>Source: {application.job.source}</p>
                        <p>Link: <a 
                            href={application.job.link}
                            target='_blank'>{application.job.link}</a></p>
                        <p>Referred by: {application.referred_by}</p>
                    </details>
                )
            )}
        </div>
    )   
}

export default Applications