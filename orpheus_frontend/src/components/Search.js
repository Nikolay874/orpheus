import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';
import {Container, Navbar, Form, FormControl, Button} from 'react-bootstrap';
import { searchByQuery } from "../transport";

function Search() {
    const [query, setQuery] = useState("")
    const navigate = useNavigate();
    const handleSearch = () => {
        navigate(`/results?query=${encodeURIComponent(query)}`);
    }

    return (
        <>
            <Container
                className="d-flex flex-column align-items-center justify-content-center"
                style={{height: '80vh'}}>
                <h1 className="mb-4">Пошук</h1>
                <Form className="w-50">
                    <FormControl type="text" placeholder="Введите запрос..."
                                 className="mb-3" value={query}
                                 onChange={(e) => setQuery(e.target.value)}/>
                    <div className="d-flex justify-content-center">
                        <Button variant="primary" className="me-2"
                                onClick={handleSearch}>Шукати</Button>
                        <Button variant="secondary">Мені повезе</Button>
                    </div>
                </Form>
            </Container>
        </>
    );
}

export default Search;