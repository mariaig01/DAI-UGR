import React, { useState } from 'react'
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

export default function Navigation({cambiado, setProductosF}) {
    const [searchTerm, setSearchTerm] = useState("");

    const handleSearch = async (event) => {
        event.preventDefault();
        const response = await fetch(`http://localhost:8000/etienda/api/searchproduct?to_find=${searchTerm}`);
        const data = await response.json();
        setProductosF(data);
    };

    return (
        <Navbar expand="lg" className="bg-body-tertiary" fixed="top">
        <Container fluid>
            <Navbar.Brand href="http://localhost:5173">DAI Commerce</Navbar.Brand>
            <Navbar.Toggle aria-controls="navbarScroll" />
            <Navbar.Collapse id="navbarScroll">
                <Nav
                    className="me-auto my-2 my-lg-0"
                    style={{ maxHeight: '100px' }}
                    navbarScroll
                >
                </Nav>
                <Form className="d-flex" onSubmit={handleSearch}>
                    <Form.Control
                        type="search"
                        placeholder="Search"
                        className="me-2"
                        aria-label="Search"
                        onChange={ (evento) => {setSearchTerm(evento.target.value)}}
                    />
                    <Button variant="outline-success" type="submit">Search</Button>
                </Form>
            </Navbar.Collapse>
        </Container>
    </Navbar>
    )
}