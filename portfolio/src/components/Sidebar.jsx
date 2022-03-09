import { Box, Typography } from '@mui/material'
import React from 'react'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardMedia from '@mui/material/CardMedia'
import { CardActionArea } from '@mui/material'
import Divider from '@mui/material/Divider'
import InterestList from './InterestList'

export default function Sidebar() {
  return (
    <Box>
      <Card>
        <CardActionArea>
          <CardMedia
            component="img"
            height="250"
            image="https://avatars.githubusercontent.com/u/3177681?v=4"
            alt="Kerem"
          />
          <CardContent>
            <Typography marginBottom={2}>
              Currently, I am working on a stealth mode startup. Previously, I
              worked at Kadir Has University as a research assistant where I got
              my master's degree.
            </Typography>

            <Divider></Divider>

            <Typography gutterBottom variant="h5" component="div">
              Interests
            </Typography>

            <InterestList></InterestList>

            <Divider></Divider>
            <Typography gutterBottom variant="h5" component="div">
              Categories
            </Typography>

            <Typography variant="body2" color="text.secondary">
              More stuff will come here.
            </Typography>
          </CardContent>
        </CardActionArea>
      </Card>
    </Box>
  )
}
