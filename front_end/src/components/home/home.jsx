import React, { Component, lazy, Suspense } from 'react'

const Filters = lazy(() => import('./filters'));
const HomeMain = lazy(() => import('./home_main'));

import Loader from '../loader'
import Loader2 from '../loader2'

class Home extends Component {

  render() {

    return (
      <div>
        <Suspense fallback={<Loader2/>}>
          <Filters/>
        </Suspense>
        <Suspense fallback={<Loader2/>}>
          <HomeMain/>
        </Suspense>
      </div>
    )
  }
}

export default Home;
