import React from 'react'
import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'

export default function Header() {
  return (
    <main>
      <div>
        <Box marginTop="60px">
          <Container maxWidth="lg">
            <Box>
              <Typography
                variant="h5"
                align="center"
                color="textPrimary"
                gutterBottom
              >
                Economics | Data Science | Programming
              </Typography>
              <Typography
                variant="h2"
                align="center"
                color="textPrimary"
                gutterBottom
              >
                Porfolio
              </Typography>
            </Box>

            <Box
              component="img"
              sx={{
                width: '100%',
                height: '450px',
                //   maxHeight: { xs: 400, md: 167 },
                objectFit: 'cover',
              }}
              alt=""
              src="https://images.unsplash.com/photo-1431411207774-da3c7311b5e8?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80"
            />
            <Typography
              variant="h5"
              align="center"
              color="textSecondary"
              margin={10}
              paragraph
            >
              Hello everyone! Thanks for stopping by. My name is Kerem. You can
              see my recent projects in this website.
            </Typography>
          </Container>
        </Box>
      </div>
    </main>
  )
}
