import React from "react"
import {useState, useEffect} from "react"

function Applications() {
    const [applications, setApplications] = useState([]);
    useEffect(() => {
        async function fetchUser() {
            console.log('in useEffect');
            const result = await fetch('/user');
            const user = await result.json();
            const applications_array = user.applications;
            console.log(applications_array);
            setApplications(
                applications_array.map(function(application) {
                    return (
                        <details key={application.application_id}>
                            <summary>{application.job.title} - {application.job.company.company_name}</summary>
                            <p>Applied: {Date(application.datetime_applied)}</p>
                            <details>
                                <summary>{application.application_statuses[0].datetime_created} - {application.application_statuses[0].status}</summary>
                                {application.application_statuses.length > 1 && 
                                application.application_statuses.slice(1).map((application_status) => 
                                <p key={application_status.application_status_id}>{application_status.datetime_created} - {application_status.status}</p>)}
                            </details>
                            <p>Link: <a 
                                href={application.job.link}
                                target='_blank'>{application.job.link}</a></p>
                            <p>Source: {application.job.source}</p>
                            <p>Referred by: {application.referred_by}</p>
                        </details>
                    )
                }
            )
            )
        }
        fetchUser();
    }, []);

    return (
        <div>
            {applications}
        </div>
    )   
}

export default Applications