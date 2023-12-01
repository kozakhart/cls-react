import React from 'react'

const ENTER_KEY_CODE = 13

export default class EditableCell extends React.Component {
  constructor(props) {
    super(props);
    this.placeholder = props.placeholder;
    this.onSave = props.onSave;
    this.state = {
      value: props.initialValue || '', // Use props.initialValue as the initial value
    };
  }

  _onChange(event) {
    const newValue = event.target.value;
    this.setState({ value: newValue });
    this.props._onChange(newValue);
    console.log(newValue);
  }

  _save() {
    this.onSave(this.state.value)
    this.setState({
      value: ''
    })
  }

  _onKeyDown(event) {
    if (event.keyCode === ENTER_KEY_CODE) {
      this._save();
    }
  }

  render() {
    return (
      <input
        type="text"
        id={this.props.id}
        onChange={this._onChange.bind(this)}
        onKeyDown={this._onKeyDown.bind(this)}
        placeholder={this.placeholder}
        value={this.state.value}
        style={{'border': 'none', borderBottom: '1px solid black',  'outline': 'none'}}
      />
    )
  }
}

