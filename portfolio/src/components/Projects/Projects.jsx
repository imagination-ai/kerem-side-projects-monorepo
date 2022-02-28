import { Container, Grid } from '@mui/material'
import React from 'react'
import { Link, Outlet } from 'react-router-dom'
import ActionAreaCard from '../ActionAreaCard/ActionAreaCard'
import projects from '../../lib/utils'

const ProjectLayout = () => {
  return (
    <div>
      <Container maxWidth="md">
        <Grid container spacing={2}>
          {projects.map((project, i) => (
            <Grid item key={i} xs={4}>
              <Link
                style={{
                  display: 'block',
                  margin: '1rem 0',
                  textDecoration: 'none',
                }}
                to={`/projects/${i}`}
                key={i}
              >
                <ActionAreaCard
                  description={project.description}
                  title={project.title}
                  url={project.url}
                  key={i}
                />
              </Link>
              <Outlet />
            </Grid>
          ))}
        </Grid>
      </Container>
    </div>
  )
}

export default class Projects extends React.Component {
  render() {
    return <ProjectLayout />
  }
}
