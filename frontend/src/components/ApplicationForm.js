import React from 'react'
import {useState, useEffect} from 'react'
import Applications from './Applications'

function ApplicationForm() {
    const initialInputs = {
        title: '',
        link: '',
        source: '',
        company_name: '',
        website: '',
        status: '',
    }
    const [inputs, setInput] = useState(initialInputs);
    const [applications, setApplications] = useState([]);

    async function fetchUser() {
        const result = await fetch('/user');
        const user = await result.json();
        setApplications(user.applications);
    }

    useEffect(() => {
        console.log('in useEffect');
        fetchUser();
    }, [])

    function handleChange(evt) {
        setInput({...inputs, [evt.target.name]: evt.target.value});
    }

    function clearFields() {
        setInput(initialInputs)
    }

    async function handleSubmit(evt) {
        evt.preventDefault();
        console.log('before fetch');
        const formData = new FormData(document.getElementById('new-application'));
        await fetch('/new-application', 
            {method: 'POST',
            body: formData,})
            .then(console.log('posted new application'))
            ;
        fetchUser();
        clearFields();

    }

    return (
        <div>
            Enter new application: 
            <form id="new-application" onSubmit={handleSubmit} method="POST">
                Status<select name="status" value={inputs.status} onChange={handleChange}>
                    <option value="" defaultValue>--Select Status--</option>
                    <option value="Pending Referral">Pending Referral</option>
                    <option value="Applied">Applied</option>
                    <option value="Phone interviewed">Phone interviewed</option>
                    <option value="Onsite interviewed">Onsite interviewed</option>
                    <option value="Rejected">Rejected</option>
                    <option value="Received Offer">Received Offer</option>
                </select>
                Title<input type="text" name="title" value={inputs.title} onChange={handleChange} />
                Link<input type="text" name="link" value={inputs.link} onChange={handleChange} />
                Source<input type="text" value={inputs.source} name="source" onChange={handleChange} />
                Company Name<input type="text" value={inputs.company_name} name="company_name" onChange={handleChange} />
                Company Website<input type="text" value={inputs.website} name="website" onChange={handleChange} />

                <input type="submit" />
            </form>
            <Applications applications={applications}/>
        </div>
    )
}

export default ApplicationForm