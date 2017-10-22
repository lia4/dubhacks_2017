import React from "react";
import { FormGroup, ControlLabel, FormControl } from "react-bootstrap";

class Submission extends React.Component {

	render() {
		return (
			<div>
				<p>This is the submission box. It should include a file upload thingy and a text box</p>
				<FormGroup controlId="formControlsTextarea" bsSize="xs">
      				<ControlLabel>Textarea</ControlLabel>
      				<FormControl componentClass="textarea" placeholder="Enter your message here..." />
    			</FormGroup>
			</div>
			
		);
	}
}

export default Submission;