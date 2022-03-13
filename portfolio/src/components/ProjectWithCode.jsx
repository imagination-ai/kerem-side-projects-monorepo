import React from 'react'

import Grid from '@mui/material/Grid'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import { CardActionArea, Chip, Link, Stack } from '@mui/material'
import Divider from '@mui/material/Divider'
import ReactMarkdown from 'react-markdown'

export default function ProjectWithCode(props) {
  return (
    <Box sx={{ flex: 1 }} m={4}>
      <Grid container spacing={1}>
        <Grid item xs={12}>
          <Typography
            variant="h2"
            textAlign={'left'}
            fontFamily="Lora"
            fontStyle={'italic'}
          >
            {props.project.title}
          </Typography>
        </Grid>
        <Grid item xs={9}>
          <Typography variant="h5" component="p" fontFamily="Lora; serif">
            {props.project.description}
          </Typography>
        </Grid>
        <Grid item xs={3}>
          <Typography
            variant="h5"
            weight="200"
            fontSize="10px"
            textAlign={'right'}
          >
            {props.date}
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Box
            component="img"
            sx={{
              height: 350,
              width: '100%',
              objectFit: 'cover',
            }}
            alt=""
            src={props.project.url}
          />
        </Grid>
        <Grid item xs={12} marginBottom={'4rem'}>
          <Card>
            <CardActionArea>
              <CardContent
                style={{
                  display: 'flex',
                  gap: '1rem',
                  height: '100%',
                }}
              >
                <Link href={props.project.repo_url}>Repo @ Github</Link>

                <Divider orientation="vertical"></Divider>

                <Stack
                  direction="row"
                  divider={<Divider orientation="vertical" flexItem />}
                  spacing={1}
                >
                  {props.project.tags.map((tag, i) => (
                    <Chip label={tag} key={i} p={2} color="primary" />
                  ))}
                </Stack>
              </CardContent>
            </CardActionArea>
          </Card>
        </Grid>

        <Grid item xs={12} md={8} paddingRight={2}>
          <ReactMarkdown children={props.text} />
        </Grid>

        {props.code}
      </Grid>
    </Box>
  )
}
