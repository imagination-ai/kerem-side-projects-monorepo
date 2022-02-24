import React, { useState } from 'react'
import { useParams } from 'react-router-dom'
import StyleClient from '../style/style_client'
import Form from 'react-bootstrap/Form'
import 'bootstrap/dist/css/bootstrap.min.css'
import Button from 'react-bootstrap/Button'
import Table from 'react-bootstrap/Table'

const client = new StyleClient(
  process.env.REACT_APP_STYLE_HOST || 'localhost',
  process.env.REACT_APP_STYLE_PORT || '8080'
)


// export function getProject (index) {
//   return projects[index]
// }

export default function StyleProject (props) {
  let params = useParams()
  // let project = getProject(parseInt(params.projectId, 10))

  const [predictions, setPredictions] = useState({})
  const [inputField, setInputField] = useState({
    text: '',
    model_name: 'mock'
  })

  const inputsHandler = e => {
    const { name, value } = e.target
    setInputField(prevState => ({
      ...prevState,
      [name]: value
    }))
  }

  const predictionToTable = prediction => {
    return (
      <tbody>
        {Object.entries(predictions).map(([key, value]) => {
          // console.log(key, value)
          return (
            <tr key={key}>
              <td></td>
              <td>{key}</td>
              <td>{value}</td>
            </tr>
          )
        })}
      </tbody>
    )
  }

  const handlePredictions = async () => {
    console.log(inputField.text)
    const results = await client.predict(inputField.text, inputField.model_name)
    setPredictions(results.data['prediction'])
    // setPredictions(JSON.stringify(results.data['prediction']))
  }

  return (
    <div>
      <h1>{props.project.title}</h1>
      <div>
        <br></br>
        <i> {props.project.description}</i>
      </div>

      <br></br>

      <p>
        What we do In this project, we created a few models with different sizes
        each of which take text as input, and returns a list of of authors. The
        bigger the probability, the closer the style of the corresponding
        author. Currently, we return only the <b>top 3 authors</b>.
      </p>
      <p>
        <b>Text:</b> "{inputField.text}"
      </p>
      <p>
        <b>Model Name:</b> "{inputField.model_name}"
      </p>

      <Table striped bordered hover>
        <thead>
          <tr>
            <th>#</th>
            <th>Author</th>
            <th>Probability</th>
          </tr>
        </thead>
        {predictionToTable(predictions)}
      </Table>

      <br></br>

      <Form>
        <Form.Group className='mb-3' controlId='formBasicEmail'>
          <Form.Label>
            Jot down or copy some text. We can tell you wrote this!
          </Form.Label>
          <Form.Control
            // type='email'
            name='text'
            value={inputField.text}
            onChange={inputsHandler}
            placeholder='It was the best of times, it was the worst of times...'
          />
          <Form.Text className='text-muted'>
            Copy or write some snippet to figure out who would be the author...
          </Form.Text>
        </Form.Group>

        <Form.Group className='mb-3' controlId='formBasicPassword'>
          <Form.Select
            aria-label='Default select example'
            name='model_name'
            value={inputField.model_name}
            onChange={inputsHandler}
          >
            <option value='small'>small-model</option>
            <option value='mock'>mock-model</option>
          </Form.Select>
        </Form.Group>

        <Button variant='primary' onClick={handlePredictions}>
          Submit
        </Button>
      </Form>
    </div>
  )
}
