import * as React from 'react';

import { FormGroup, ControlLabel, FormControl, Button, Glyphicon } from 'react-bootstrap';

interface SearchBarProps { onSubmit: ((query: String) => void)}
interface SearchBarState { query: string }

export default class SearchBar extends React.Component<SearchBarProps,SearchBarState> {
    constructor (props: any) {
        super(props)
        this.state = {
          query: ''
        }
        this.handleChange = this.handleChange.bind(this);
        this.handleClick = this.handleClick.bind(this);
      }
    
    handleChange (event: any) {
        this.setState({query: event.target.value});
    }

    handleClick (event: any) {
        this.props.onSubmit(this.state.query);
    }

    render () {
        return (
            <div className='searchbar-container'>
                <input type='text'
                    placeholder='Search Query'
                    value={this.state.query}
                    onChange={this.handleChange}/>
                <button
                    type='button'
                    onClick={this.handleClick}>
                    <Glyphicon glyph="search"/>
                </button>
            </div>
        )
    }
}
