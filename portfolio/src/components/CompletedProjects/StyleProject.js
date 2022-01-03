import React, { useState } from 'react'
import { useParams } from 'react-router-dom'
import MarkdownTranslator from '../MarkdownTranslator/MarkdownTranslator'
import { getProject } from '../Projects/Projects'
import StyleClient from '../../utils/style/style_client'

const client = new StyleClient(
  process.env.REACT_APP_STYLE_HOST || 'localhost',
  process.env.REACT_APP_STYLE_PORT || '8080'
)

const content = `# What we do 

In this project, we created a few models with different sizes each of
which take text as input, and returns a list of of authors.
The bigger the probability, the closer the style of the corresponding author. 

Currently, we returns only the **top 3 authors**.

`

export default function StyleProject (props) {
  let params = useParams()
  let project = getProject(parseInt(params.projectId, 10))

  const [predictions, setPredictions] = useState({})
  const [inputField, setInputField] = useState({
    text: '',
    model_name: ''
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
      <table>
        <tbody>
          <tr>
            <th>Author</th>
            <th>Probability</th>
          </tr>
          {Object.entries(predictions).map(([key, value]) => {
            console.log(key, value)
            return (
              <tr key={key}>
                <td>{key}</td>
                <td>{value}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    )
  }

  const handlePredictions = async () => {
    const results = await client.predict(inputField.text, inputField.model_name)
    setPredictions(results.data['prediction'])
    // setPredictions(JSON.stringify(results.data['prediction']))
  }

  return (
    <div>
      <h1>{project.title}</h1>
      <div> {project.description}</div>
      {<MarkdownTranslator>{content}</MarkdownTranslator>}

      <p>Text: {inputField.text}</p>
      <p>Model Name: {inputField.model_name}</p>
      <div>{predictionToTable(predictions)}</div>
      <div>
        <input
          type='text'
          name='text'
          onChange={inputsHandler}
          placeholder='Text?'
          value={inputField.text}
        />

        <br />

        <input
          type='text'
          name='model_name'
          onChange={inputsHandler}
          placeholder='Model Name?'
          value={inputField.model_name}
        />

        <br />

        <button onClick={handlePredictions}>Submit Now</button>
      </div>
    </div>
  )
}
