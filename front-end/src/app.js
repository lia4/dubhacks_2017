import React from "react";
import Header from "./components/header"

import "./styles/app.css"

class App extends React.Component {

    render() {
        return (
            <div class="App">
                <header class="App-header">
                    <Header />
                </header>
                <div id="style-wrapper">
                    <div class="style-inner-left">
                        <Header />
                    </div>
                    <div class="style-inner-right">
                        <Header />
                    </div>
                </div>
            </div>
        );
    }
}

export default App;