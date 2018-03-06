import * as React from 'react';
import { BrowserRouter, Route, Switch, Link, NavLink } from 'react-router-dom';

import Header from '../components/Header';
import { Hello } from '../components/Hello';

export default class AppRouter extends React.Component<{}, {}> {
    render() {
        return (
            <BrowserRouter>
                <div>
                    <Header />
                    <Switch>
                        <Route path="/" component={Hello}/>
                    </Switch>
                </div>
            </BrowserRouter>);
    }
};