import * as React from 'react'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardMedia from '@mui/material/CardMedia'
import Typography from '@mui/material/Typography'
import { CardActionArea } from '@mui/material'

import image from '../../assets/images/shakespeare.jpeg'

export default function ActionAreaCard (props) {
    console.log(props.url)

  return (
    <Card sx={{ maxWidth: 345, display: 'flex', flexDirection: 'column' }}>
      <CardActionArea>
        <CardMedia
          component='img'
          height='140'
          image={props.url}
        />
        <CardContent>
          <Typography gutterBottom variant='h5' component='div'>
            {props.title}
          </Typography>
          <Typography variant='body2' color='text.secondary'>
            {props.description}
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  )
}
