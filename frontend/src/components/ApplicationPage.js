import React from 'react'
import {useState, useEffect} from 'react'
import Applications from './Applications'
import ApplicationForm from './ApplicationForm'

function ApplicationPage() {
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
        setInput(initialInputs)

    }

    return (
        <div>
            <ApplicationForm 
                handleChange={handleChange}
                handleSubmit={handleSubmit} 
                inputs={inputs} 
                setInput={setInput}
                initialInputs={initialInputs}
            />
            <Applications 
                applications={applications}
                setApplications={setApplications}
                fetchUser={fetchUser}
            />
        </div>
    )
}

export default ApplicationPage