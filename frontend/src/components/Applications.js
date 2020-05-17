import React from "react"
import {useState} from "react"
import moment from "moment"

function StatusChange(props) {
    const [new_status, setStatus] = useState(props.new_status);
    function handleChange(evt) {
        setStatus(evt.target.value);
        console.log(props.application_id, "new status state:", new_status);
    }
    async function handleSubmit(evt) {
        evt.preventDefault();
        console.log(props.application_id, "new status state:", new_status);
        const formData = new FormData();
        formData.append('new_status', new_status);
        formData.append('application_id', props.application_id);
        console.log(...formData);
        await fetch('/new-application-status',
            {method: 'POST',
            body: formData})
            .then(console.log('posted new status'))
            .then(props.fetchUser);
    }
    return (
        <form id="change-status" onSubmit={handleSubmit} method="POST">
            <select name="status" value={new_status} onChange={handleChange}>
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
                        <p>Applied: {moment(application.datetime_applied).toString()}</p>
                        Current Status: <StatusChange 
                            new_status={application.application_statuses[0].status} 
                            application_id={application.application_id}
                            fetchUser={props.fetchUser}/>
                        <details>
                            <summary>Status History</summary>
                            {application.application_statuses.map((application_status) => 
                            <p key={application_status.application_status_id}>{moment(application_status.datetime_created).toString()} - {application_status.status}</p>)}
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