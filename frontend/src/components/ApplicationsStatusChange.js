import React from "react"
import {useState} from "react"
import moment from "moment"

function ApplicationsStatusChange(props) {
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

export default ApplicationsStatusChange