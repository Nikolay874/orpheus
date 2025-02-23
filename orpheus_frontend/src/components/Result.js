import React, {useState, useEffect} from "react";
import {
    Container,
    Form,
    Button,
    Navbar,
    Card,
    Pagination
} from "react-bootstrap";
import {Prism as SyntaxHighlighter} from "react-syntax-highlighter";
import {darcula} from "react-syntax-highlighter/dist/esm/styles/prism";
import {useLocation} from 'react-router-dom';
import {searchByQuery} from "../transport";
import { useNavigate } from 'react-router-dom';

function useQuery() {
    return new URLSearchParams(useLocation().search);
}



const Results = () => {
    const queryParam = useQuery().get("query") || "";
    const [query, setQuery] = useState(queryParam);
    const [results, setResults] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const resultsPerPage = 2;
    const navigate = useNavigate();


    useEffect(() => {
        searchByQuery(query).then((data) => {
                setResults(data);
            }
        )
    }, []);

    // Определение видимых результатов на текущей странице
    const indexOfLastResult = currentPage * resultsPerPage;
    const indexOfFirstResult = indexOfLastResult - resultsPerPage;
    const currentResults = results.slice(indexOfFirstResult, indexOfLastResult);

    const handleSearch = (e) => {
        e.preventDefault();
        searchByQuery(query).then((data) => {
                setResults(data);
            }
        )
        console.log("Ищем:", query);
    };

    const handleTitleClick = (id, index) => {
        navigate(`/code_viewer?id=${encodeURIComponent(id)}&index=${encodeURIComponent(index)}`)
    };

    const nextPage = () => setCurrentPage((prev) => Math.min(prev + 1, Math.ceil(results.length / resultsPerPage)));
    const prevPage = () => setCurrentPage((prev) => Math.max(prev - 1, 1));

    return (
        <div>
            <Navbar bg="light" expand="lg">
                <Container>
                    <Navbar.Brand href="/">Пошук коду</Navbar.Brand>
                </Container>
            </Navbar>
            <Container className="mt-4">
                <Form
                    onSubmit={handleSearch}
                    className="d-flex">
                    <Form.Control
                        type="text"
                        placeholder="Введіть ваш запит..."
                        className="me-2"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                    <Button
                        type="submit"
                        variant="primary">
                        Шукати
                    </Button>
                </Form>
                <div className="mt-4">
                    {currentResults.map((result, index) => (
                        <Card key={index} className="mb-3">
                            <Card.Body>
                                <Card.Title>
                                    <a
                                        href="#"
                                        onClick={(e) => {
                                            e.preventDefault();
                                            handleTitleClick(result.id, result.index);
                                        }}
                                        style={{
                                            textDecoration: "none",
                                            color: "blue",
                                            cursor: "pointer"
                                        }}
                                    >
                                        {result.title}
                                    </a>
                                </Card.Title>
                                <SyntaxHighlighter language={result.language}
                                                   style={darcula}>
                                    {result.code}
                                </SyntaxHighlighter>
                            </Card.Body>
                        </Card>
                    ))}
                </div>
                <Pagination className="justify-content-center">
                    <Pagination.Prev onClick={prevPage}
                                     disabled={currentPage === 1}/>
                    <Pagination.Item active>{currentPage}</Pagination.Item>
                    <Pagination.Next onClick={nextPage}
                                     disabled={indexOfLastResult >= results.length}/>
                </Pagination>
            </Container>
        </div>
    );
};

export default Results;
