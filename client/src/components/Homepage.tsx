import * as React from 'react';
import { Grid, Row, Col } from 'react-bootstrap';

import SearchBar from './SearchBar';

export default class Homepage extends React.Component<{}, {}> {
    handleSubmit (query: string) {
        alert(query);
    }

    render () {
        return (
            <div className="outer">
                <div className="middle">
                    <div className="inner">
                    <Grid>
                        <Row className="show-grid">
                            <Col xs={1} md={4}></Col>
                            <Col xs={4} md={4}>
                                <SearchBar onSubmit={this.handleSubmit}/>
                            </Col>
                            <Col xs={1} md={4}></Col>
                        </Row>
                    </Grid>
                    </div>
                </div>
            </div>
            
        );
    }
}