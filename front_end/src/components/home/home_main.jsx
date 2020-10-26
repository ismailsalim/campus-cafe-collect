import React, { Component, lazy, Suspense } from 'react'

const HomeMobile = lazy(() => import('./home_mobile'));
const HomeDesktop = lazy(() => import('./home_desktop'));

import Loader from '../loader'

class HomeMain extends Component {
  constructor() {
      super();
      this.state = {
        width: window.innerWidth,
      };
    }

    componentDidMount() {
      window.addEventListener('resize', this.handleWindowSizeChange);
    }

    // make sure to remove the listener
    // when the component is not mounted anymore
    componentWillUnmount() {
      window.removeEventListener('resize', this.handleWindowSizeChange);
    }

    handleWindowSizeChange = () => {
      this.setState({ width: window.innerWidth });
  };

  render() {
    const { width } = this.state;
    const isMobile = width <= 600;

      if (isMobile) {
        return (
          <Suspense fallback={<Loader/>}>
            <div className="home-main">
              <HomeMobile/>
            </div>
          </Suspense>
        );
      } else {
        return (
          <Suspense fallback={<Loader/>}>
            <div className="home-main">
              <HomeDesktop/>
            </div>
          </Suspense>
        );
      }
  }
}

export default HomeMain;
