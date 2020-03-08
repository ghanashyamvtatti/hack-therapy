import React, { Component } from "react";
import { Widget, addResponseMessage, toggleWidget, renderCustomComponent } from "react-chat-widget";
import logo from "./boticon.png";
import userIng from "./bobcat.png";
import "./App.css";
import "react-chat-widget/lib/styles.css";
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Select from 'react-select';
import Microlink from '@microlink/react';


class App extends Component {
  constructor(props) {
    super(props);


    this.state = {
      context: {},
      show: true,
      finalArr: [],
      selectedArr: []
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
  }

  handleNewUserMessage = newMessage => {
    console.log(`New message incomig! ${newMessage}`);
    // Now send the message throught the backend API
    this.sendMessage(newMessage).then(response =>{
      addResponseMessage(response["message"])
       if(Object.keys(this.state.context).includes("memes")){
          renderCustomComponent(Microlink, {url: this.state.context.memes});
          renderCustomComponent(Microlink, {url: this.state.context.music});
          var context = this.state.context;
          delete this.state.context.memes;
          delete this.state.context.music;
          this.setState({context: context});
       }
    });
  };

  toggleShow(){
    
    this.setState({
      show: !this.state.show
    });
  }

   storeInLocal(name, subjects){
     localStorage.setItem('name', name);
     localStorage.setItem('subjects', subjects);
   }

  onModalClose() {
    this.setState({show: false});
    toggleWidget();
  }

  render() {

    let modal = (<Modal 
                size="lg"
                aria-labelledby="contained-modal-title-vcenter"
                centered
                show={this.state.show} onHide={() => this.toggleShow}>
                  <Modal.Header >
                    <Modal.Title id="contained-modal-title-vcenter">Please provide us some details so we can help you</Modal.Title>
                  </Modal.Header>
                  <Modal.Body>
                    <form>
                      <div className="form-group">
                        <label >Name:</label><br/>
                        <input type="text" id="name" name="name" className="input-style" /><br/><br />
                      </div>
                      <Select options={this.state.finalArr} isMulti onChange={selectedOption => {this.setState({selectedArr: selectedOption})}}/>
                    </form>

                  </Modal.Body>
                  <Modal.Footer>
                  <Button variant="primary" onClick={() => {
                    this.setState({show: false});
                    toggleWidget();
                    var context = this.state.context;
                    context['courses'] = this.state.selectedArr;
                    this.setState({context: context});
                    console.log(this.state.context);  
                  }}>
                    Save
                    </Button>
                  </Modal.Footer>
                </Modal>)
    return (
      <div className="App">
        {this.state.show ? modal: null}
        
        <Widget
          fullScreenMode={true}
          showCloseButton={false}
          profileAvatar={logo}
          handleNewUserMessage={this.handleNewUserMessage}
        />
      </div>
    );
  }
}

export default App;
