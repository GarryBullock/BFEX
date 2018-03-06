import * as React from 'react';
import { NavLink } from 'react-router-dom';

export default class Header extends React.Component<{}, {}> {
    render() {
        return (
          <nav className="navbar navbar-default navbar-fixed-top">
            <div className="container">
              <div className="navbar-header">
                <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                  <span className="sr-only">Toggle navigation</span>
                  <span className="icon-bar"></span>
                  <span className="icon-bar"></span>
                  <span className="icon-bar"></span>
                </button>
                <a className="navbar-brand" href="/">Better Find-an-Expert</a>
              </div>
              <div id="navbar" className="collapse navbar-collapse navbar-right">
                <ul className="nav navbar-nav">
                  <li>
                    <NavLink to="/" activeClassName="is-active" exact={true}>Home</NavLink>
                  </li>
                  <li>
                    <NavLink to="/about" activeClassName="is-active">About</NavLink>
                  </li>
                </ul>
              </div>
            </div>
          </nav>
        );
      }
}