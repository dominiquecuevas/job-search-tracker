import React from "react"
import {useState} from "react"

function StatusChange(props) {
    const [status, setStatus] = useState(props.current_status);
    function handleChange(evt) {
        setStatus(evt.target.value);
        console.log(props.application_id, "new status state:", status);
    }
    async function handleSubmit(evt) {
        evt.preventDefault();
        console.log(props.application_id, "new status state:", status);
        const formData = new FormData();
        formData.append('new_status', status);
        formData.append('application_id', props.application_id);
        console.log(...formData);
        await fetch('/new-application-status',
            {method: 'POST',
            body: formData})
            .then(console.log('posted new status'));
    }
    return (
        <form id="change-status" onSubmit={handleSubmit} method="POST">
            <select name="status" value={status} onChange={handleChange}>
                <option value="Pending Referral">Pending Referral</option>
                <option value="Applied">Applied</option>
                <option value="Phone interviewed">Phone interviewed</option>
                <option value="Onsite interviewed">Onsite interviewed</option>
                <option value="Rejected">Rejected</option>
                <option value="Received Offer">Received Offer</option>
            </select>
            <input type="submit" value="Update Status"/>
        </form>
    )
}

function Applications(props) {
    return (
        <div>
            {props.applications.map(
                application => (
                    <details key={application.application_id}>
                        <summary>{application.job.title} - {application.job.company.company_name}</summary>
                        <p>Applied: {Date(application.datetime_applied)}</p>
                        <p>Current Status: {application.application_statuses[0].status}</p>
                        <StatusChange current_status={application.application_statuses[0].status} application_id={application.application_id}/>
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