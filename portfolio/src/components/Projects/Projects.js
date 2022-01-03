import React from 'react'
import classes from './Projects.module.css'
import ProjectCard from '../ProjectCard/ProjectCard'
import { Link, Outlet } from 'react-router-dom'

const projects = [
  {
    title: 'Writing Style Prediction',
    description: 'Check which author is influenced by you.'
  },
  {
    title: 'Inflation in Turkey',
    description: 'What would you say if I tell you the real inflation?'
  },
  { title: 'Project Placeholder', description: 'This project is ....' },
  { title: 'Another project', description: 'Some description' },
  {
    title: 'Inflation in Turkey',
    description: 'What would you say if I tell you the real inflation?'
  },
  { title: 'Project Placeholder', description: 'This project is ....' },
  { title: 'Another project', description: 'Some description' }
]



export function getProject (index) {
  return projects[index]
}

export default class Projects extends React.Component {
  render () {
    return (
      <div className={classes.cards}>
          {projects.map((project, i) => (
            <Link
              style={{ display: 'block', margin: '1rem 0' }}
              to={`/projects/${i}`}
              key={i}
            >
              <ProjectCard
                description={project.description}
                title={project.title}
                key={i}
              />
            </Link>
          ))}
        <Outlet />
      </div>
    )
  }
}
