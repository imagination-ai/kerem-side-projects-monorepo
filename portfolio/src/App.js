import './App.module.css'

import Layout from './components/Layout/Layout'
import React, { Component } from 'react'
import { Route, Routes } from 'react-router-dom'
import Projects from './components/Projects/Projects'
import StyleProject from './components/CompletedProjects/StyleProject'

export default class App extends Component {
  render () {
    let routes = (
      <Routes>
        <Route path='/' element={<div>This is the home page</div>} />
        <Route path='/projects' element={<Projects />} />
        <Route path='/projects/:projectId' element={<StyleProject />} />
        <Route path='/about' element={<div>About Kerem Baskaya</div>} />
        <Route
          path='*'
          element={
            <main style={{ padding: '1rem' }}>
              <p>
                Something went wrong. We could not find the project article!
              </p>
            </main>
          }
        />
      </Routes>
    )

    return <Layout>{routes}</Layout>
  }
}
