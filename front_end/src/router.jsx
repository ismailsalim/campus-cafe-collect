import React, { Component, lazy, Suspense } from 'react'
import { BrowserRouter, Route, Redirect, Switch, withRouter } from 'react-router-dom';
import { createHistory as history } from 'history';

import routes from './routes';

const Home = lazy(() => import('./components/home/home'));
const VenuePage = lazy(() => import('./components/venue_page/venue_page'));
const Success = lazy(() => import('./components/basket/success'));
const LandingPage = lazy(() => import('./components/landing/landing'));
const NavBar = lazy(() => import('./components/navbar'));
const ErrorPage = lazy(() => import('./components/landing/error'));

import Loader from './loader'


class Router extends Component {

  loader = () => {
    return (<div className="loader">
              <div data-v-21dcae14="" className="box" category="animation" text=""><div data-v-21dcae14="" className="bouncingLoader"><div data-v-21dcae14=""></div></div></div>
            </div>)
  }


  render() {

    // const routeComponents = routes.map(({path, component}, key) => <Route exact path={path} component={component} key={key} />);
    return (
      <Suspense fallback={<Loader/>}>
        <BrowserRouter>
            <NavBar/>
            <Switch>
              <Route  path="/" exact component={LandingPage}  />
              <Route  path="/home" component={Home}  />
              <Route  path="/venues/:venueid/:typeid" component={VenuePage}  />
              <Route  path="/success" component={Success}  />
              <Route component={ErrorPage} />
            </Switch>
        </BrowserRouter>
      </Suspense>
    )
  }
}

export default Router;
