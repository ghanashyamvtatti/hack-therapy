import React, { Component } from "react";
import { Widget, addResponseMessage, toggleWidget } from "react-chat-widget";
import logo from "./logo.svg";
import "./App.css";
import "react-chat-widget/lib/styles.css";

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      context: {}
    };
  }
  sendMessage(message) {
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json"
      },
      body: JSON.stringify({ message: message, context: this.state.context })
    };
    return fetch(
      "https://us-central1-neural-sunup-253704.cloudfunctions.net/witai",
      requestOptions
    )
      .then(response => response.json())
      .then(responseBody => {
        this.setState({ context: responseBody["context"] });
        console.log(this.context);
        return responseBody;
      })
      .catch(error => console.log(error));
  }
  componentDidMount() {
    this.sendMessage("").then(response =>
      addResponseMessage(response["message"])
    );
    toggleWidget();
    this.setState();
  }
  handleNewUserMessage = newMessage => {
    console.log(`New message incomig! ${newMessage}`);
    // Now send the message throught the backend API
    this.sendMessage(newMessage).then(response =>
      addResponseMessage(response["message"])
    );
  };
  render() {
    return (
      <div className="App">
        <Widget
          fullScreenMode={true}
          showCloseButton={false}
          handleNewUserMessage={this.handleNewUserMessage}
        />
      </div>
    );
  }
}

export default App;
