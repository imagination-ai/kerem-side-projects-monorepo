import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'
import React, { Component } from 'react'
import { Route, Routes } from 'react-router-dom'
import Projects from './components/Projects/Projects'
import ResponsiveAppBar from './components/ResponsiveAppBar'
import StyleProject from './components/StyleProject'
import projects from './style/utils'

const Layout = props => {
  return (
    <>
      <ResponsiveAppBar></ResponsiveAppBar>
      {props.child}
    </>
  )
}

export default class App extends Component {
  render () {
    let routes = (
      <Routes>
        <Route
          path='/'
          element={
            <main>
              <div>
                <Container maxWidth='lg'>
                  <Typography
                    variant='h2'
                    align='center'
                    color='textPrimary'
                    gutterBottom
                  >
                    Porfolio
                  </Typography>
                  <Typography
                    variant='h5'
                    align='center'
                    color='textSecondary'
                    paragraph
                  >
                    Hello everyone! Thanks for stopping by. My name is Kerem.
                    You can see my recent projects in this website.
                  </Typography>
                </Container>
              </div>
            </main>
          }
        />
        <Route path='/projects' element={<Projects />} />
        // Blog Posts
        <Route
          path={`/projects/0`}
          element={<StyleProject project={projects[0]} />}
        />
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
          path='/about'
          element={
            <Typography variant='h5'>I was born in 1987 in Izmir.</Typography>
          }
        />
        <Route
          path='*'
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
