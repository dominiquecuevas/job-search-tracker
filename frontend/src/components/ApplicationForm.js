import React from 'react'
import {useState, useEffect} from 'react'
import Applications from './Applications'

function ApplicationForm(props) {

    return (
        <div>
            Enter new application: 
            <form id="new-application" onSubmit={props.handleSubmit} method="POST">
                Status<select name="status" value={props.inputs.status} onChange={props.handleChange}>
                    <option value="" defaultValue>--Select Status--</option>
                    <option value="Pending Referral">Pending Referral</option>
                    <option value="Applied">Applied</option>
                    <option value="Phone interviewed">Phone interviewed</option>
                    <option value="Onsite interviewed">Onsite interviewed</option>
                    <option value="Rejected">Rejected</option>
                    <option value="Received Offer">Received Offer</option>
                </select>
                Title<input type="text" name="title" value={props.inputs.title} onChange={props.handleChange} />
                Link<input type="text" name="link" value={props.inputs.link} onChange={props.handleChange} />
                Source<input type="text" value={props.inputs.source} name="source" onChange={props.handleChange} />
                Company Name<input type="text" value={props.inputs.company_name} name="company_name" onChange={props.handleChange} />
                Company Website<input type="text" value={props.inputs.website} name="website" onChange={props.handleChange} />

                <input type="submit" />
            </form>
        </div>
    )
}

export default ApplicationForm