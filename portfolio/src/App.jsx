import React, { Component } from 'react'
import { Route, Routes } from 'react-router-dom'
import Projects from './components/Projects/Projects'
import ResponsiveAppBar from './components/ResponsiveAppBar'
import StyleProject from './components/StyleProject'
import projects from './lib/utils'
import Typography from '@mui/material/Typography'
import Home from './components/pages/Home'

const Layout = (props) => {
  return (
    <>
      <ResponsiveAppBar></ResponsiveAppBar>
      {props.child}
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
          element={<StyleProject project={projects[1]} />}
        />
        <Route
          path={`/projects/2`}
          element={<StyleProject project={projects[2]} />}
        />
        <Route
          path={`/projects/3`}
          element={<StyleProject project={projects[3]} />}
        />
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
    return <Layout child={routes}></Layout>
  }
}
