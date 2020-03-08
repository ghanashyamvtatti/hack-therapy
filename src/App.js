import React, { Component } from "react";
import { Widget, addResponseMessage, toggleWidget } from "react-chat-widget";
import logo from "./logo.svg";
import "./App.css";
import "react-chat-widget/lib/styles.css";
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Select from 'react-select';

class App extends Component {
  constructor(props) {
    super(props);


    this.state = {
      context: {},
      show: true,
      finalArr: []
    };
  }

  formatDate(){
    var tempArr=this.state.filteredData;
    var finalArr={}
    for(var i=0;i<tempArr.length;i++){
      finalArr[i]={
        label : tempArr[i].course_title,
        value : tempArr[i].course_id
      }
    }

    this.setState({
      finalArr: finalArr
    });
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
  
  getCourses(message) {
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json"
      },
      body: JSON.stringify({ message: message})
    };
    return fetch(
      "https://us-central1-neural-sunup-253704.cloudfunctions.net/getcourses",
      requestOptions
    )
      .then(response => response.json())
      .then(data => {
        // const filteredData = data.filter(element => {
        //   return {label: element.course_title,value: element.course_id};
        // });
        var filteredData=[]
        for( var entry in data){
          filteredData.push({
            label: data[entry].course_title,
            value: data[entry].course_id
          })
        }

        console.log(filteredData)

        this.setState({
          finalArr: filteredData
        });
      }).catch(error => console.log(error));
  }

  componentDidMount() {
    this.getCourses("")
    this.sendMessage("").then(response =>
      addResponseMessage(response["message"])
    );
    //TODO:toggleWidget();
    this.setState();
  }

  handleNewUserMessage = newMessage => {
    console.log(`New message incomig! ${newMessage}`);
    // Now send the message throught the backend API
    this.sendMessage(newMessage).then(response =>
      addResponseMessage(response["message"])
    );
  };

  toggleShow(){
    this.setState({
      show:!this.state.show
    })
  }

  storeInLocal(name, subjects){
    localStorage.setItem('name', name);
    localStorage.setItem('subjects', subjects);
  }

  render() {
    return (
      <div className="App">
        <Modal show={this.state.show} onHide={() => this.toggleShow}>
          <Modal.Header >
            <Modal.Title>Please provide us some details so we can help you</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <form>
              <label for="name">Name:</label><br/>
              <input type="text" id="name" name="name" /><br/>
              <Select options={this.state.finalArr} isMulti />
              
              <Button variant="primary" type="submit" onClick={this.storeInLocal(name, subjects)}>
                Submit
              </Button>
            </form>

          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" >
              Close
            </Button>
            <Button variant="primary" >
              Save Changes
            </Button>
          </Modal.Footer>
        </Modal>
        
        <Widget
          fullScreenMode={true}
          showCloseButton={false}
          handleNewUserMessage={this.handleNewUserMessage}
          title="Hack Therapy"
          subtitle="A friend in need is a friend indeed"
        />

      </div>
    );
  }
}

export default App;
