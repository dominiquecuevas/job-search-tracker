import React from "react"
import {useState, useEffect} from "react"
import Alert from "react-bootstrap/Alert"
import Modal from "react-bootstrap/Modal"
import Form from "react-bootstrap/Form"
import Button from "react-bootstrap/Button"

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [show, setShow] = useState(false);
    const [validated, setValidated] = useState(false);
    const [loggedIn, setLoggedIn] = useState("");

    const handleClose = () => {
        setShow(false);
        setValidated(false);
        setEmail("");
        setPassword("");
    }
    const handleShow = (evt) => {
        evt.preventDefault();
        setShow(true);
    }

    function handleChange(evt) {
        if (evt.target.name==='email') {
            setEmail(evt.target.value)
        } else if (evt.target.name==='password') {
            setPassword(evt.target.value)
        }
    }
    function handleSubmit(evt) {
        evt.preventDefault();
        const formData = new FormData(document.getElementById('login-form'));
        fetch('/login', 
            {method: 'POST',
            body: formData,})
            .then(resp => {
                console.log('in handleSubmit login', resp);
                if (!resp.ok) {
                    setValidated(true);
                } else {
                    handleClose();
                    setLoggedIn(true);
                }
            })
            // TODO: logged in alert
            ;
    }

    function logOut(evt) {
        evt.preventDefault();
        fetch('/logout');
        setLoggedIn(false);
        // TODO: modal and alert
    }

    function loginCheck() {
        fetch('/login-check')
        .then(resp => resp.json())
        .then(resp => {
            console.log('in LoginCheck, resp:', resp);
            if (resp === false) {
                setLoggedIn(false);
                console.log('loggedIn state should be false:', loggedIn);
            } else if (resp === true) {
                setLoggedIn(true);
                console.log('loggedIn state should be true:', loggedIn);
            }
        })
    }

    useEffect(() => {
        loginCheck()
    }, [])
    
    return (
        <div>
            {loggedIn === '' ? ('') : 
                (!loggedIn ? (<a href="#" onClick={handleShow}>Login</a>) : (<a href="#" onClick={logOut}>Logout</a>))}
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Log-in</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form onSubmit={handleSubmit} id="login-form" method="POST">
                        <Form.Group controlId="formBasicEmail">
                            <Form.Label>Email address</Form.Label>
                            <Form.Control type="email" placeholder="Enter email" value={email} onChange={handleChange} name='email'/>
                        </Form.Group>
                        <Form.Group controlId="formBasicPassword">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="password" placeholder="Password" value={password} onChange={handleChange} name='password'/>
                        </Form.Group>
                        {validated && (<Form.Text className="text-muted">
                            Incorrect email address or password, try again.
                        </Form.Text>)}
                        <Button variant="primary" type="submit">
                            Submit
                        </Button>
                    </Form>
                </Modal.Body>
            </Modal>
            {/* <Alert variant="success">
                <Alert.Heading>Hey, nice to see you</Alert.Heading>
                <p>
                    Aww yeah, you successfully read this important alert message. This example
                    text is going to run a bit longer so that you can see how spacing within an
                    alert works with this kind of content.
                </p>
                <hr />
                <p className="mb-0">
                    Whenever you need to, be sure to use margin utilities to keep things nice
                    and tidy.
                </p>
            </Alert> */}
        </div>
    )
}

export default Login