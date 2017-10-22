import React from "react";
import Header from "./components/header";
import Submission from "./containers/submission";
import Result from "./containers/result";
import { Grid, Col } from "react-bootstrap";

import "./styles/app.css";

class App extends React.Component {

    render() {
        return (
            <div class="App">
                <header class="App-header">
                    <Header />
                </header>
                <Grid>
                    <Col sm={4} smOffset={1}>
                        <Submission />
                    </Col>
                    <Col sm={4} smOffset={2}>
                        <Result />
                    </Col>
                </Grid>
            </div>
        );
    }
}

export default App;