import React from "react"

function Applications(props) {
    return (
        <div>
            {props.applications.map(
                application => (
                    <details key={application.application_id}>
                        <summary>{application.job.title} - {application.job.company.company_name}</summary>
                        <p>Applied: {Date(application.datetime_applied)}</p>
                        <p>Current Status: {application.application_statuses[0].status}</p>
                        <details>
                            <summary>Status History</summary>
                            {application.application_statuses.map((application_status) => 
                            <p key={application_status.application_status_id}>{application_status.datetime_created} - {application_status.status}</p>)}
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