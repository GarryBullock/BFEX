import * as React from 'react';
import { BrowserRouter, Route, Switch, Link, NavLink } from 'react-router-dom';

import Header from '../components/Header';
import HomePage from '../components/Homepage';

export default class AppRouter extends React.Component<{}, {}> {
    render() {
        return (
            <BrowserRouter>
                <div>
                    <Header />
                    <Switch>
                        <Route path="/" component={HomePage}/>
                    </Switch>
                </div>
            </BrowserRouter>);
    }
};