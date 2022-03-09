import React, { Component } from 'react'
import { Route, Routes } from 'react-router-dom'
import ResponsiveAppBar from './components/ResponsiveAppBar'
import StyleProject from './components/StyleProject'
import projects from './lib/utils'
import Typography from '@mui/material/Typography'
import Home from './components/pages/Home'
import ScrollToTop from './components/ScrollToTop'

const Layout = (props) => {
  return (
    <>
      <ResponsiveAppBar></ResponsiveAppBar>
      <div
        style={{
          flexGrow: 1,
          maxWidth: '1600px',
          width: '80%',
          margin: '0 auto',
        }}
      >
        {props.child}
      </div>
    </>
  )
}

export default class App extends Component {
  render() {
    let routes = (
      <Routes>
        <Route path="/" element={<Home></Home>} />
        <Route
          path={`/projects/1`}
          element={<StyleProject project={projects[0]} />}
        />
        {/* <Route
          path={`/projects/2`}
          element={<StyleProject project={projects[1]} />}
        />
        <Route
          path={`/projects/3`}
          element={<StyleProject project={projects[2]} />}
        /> */}
        <Route
          path="/about"
          element={
            <Typography variant="h5">I was born in 1987 in Izmir.</Typography>
          }
        />
        <Route
          path="*"
          element={
            <main style={{ padding: '1rem' }}>
              <Typography>
                Something went wrong. We could not find the project article!
              </Typography>
            </main>
          }
        />
      </Routes>
    )
    return (
      <ScrollToTop>
        <Layout child={routes}></Layout>
      </ScrollToTop>
    )
  }
}
