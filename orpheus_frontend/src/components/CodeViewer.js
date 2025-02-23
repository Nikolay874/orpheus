import React, {useEffect, useState} from "react";
import { Container, Form, Dropdown, DropdownButton } from "react-bootstrap";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import {
  darcula,
  atomDark,
  coy,
  tomorrow,
  solarizedlight,
} from "react-syntax-highlighter/dist/esm/styles/prism";
import {useLocation} from "react-router-dom";
import {getContent, searchByQuery} from "../transport";

const themes = {
  Darcula: darcula,
  AtomDark: atomDark,
  Coy: coy,
  Tomorrow: tomorrow,
  SolarizedLight: solarizedlight,
};

function useQuery() {
    return new URLSearchParams(useLocation().search);
}

const CodeViewer = () => {
    const queryId = useQuery().get("id")
    const queryIndex = useQuery().get("index")
    const [theme, setTheme] = useState(darcula);
    const [language, setLanguage] = useState("")

    const [code, setCode] = useState("");
    useEffect(() => {
        getContent(queryId, queryIndex).then((data) => {
                setCode(data.code);
                setLanguage(data.language)
            }
        )
    }, []);
  return (
    <Container className="mt-4">
      <h3>Просмотр коду</h3>
      <DropdownButton title="Выбрать тему" variant="secondary" className="mb-3">
        {Object.keys(themes).map((themeName) => (
          <Dropdown.Item key={themeName} onClick={() => setTheme(themes[themeName])}>
            {themeName}
          </Dropdown.Item>
        ))}
      </DropdownButton>
      <SyntaxHighlighter language={language} style={theme} showLineNumbers>
        {code}
      </SyntaxHighlighter>
    </Container>
  );
};

export default CodeViewer;