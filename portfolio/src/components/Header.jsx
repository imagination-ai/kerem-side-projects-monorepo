import React from 'react'
import Container from '@mui/material/Container'
import Box from '@mui/material/Box'

export default function Header() {
  return (
    <Box>
      <Container disableGutters={true}>
        <Box
          component="img"
          sx={{
            width: '100%',
            height: '450px',
            objectFit: 'cover',
          }}
          alt=""
          src="https://images.unsplash.com/photo-1431411207774-da3c7311b5e8?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80"
        />
      </Container>
    </Box>
  )
}
