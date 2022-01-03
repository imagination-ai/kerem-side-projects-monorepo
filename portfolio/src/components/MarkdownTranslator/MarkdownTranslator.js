import React from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

const markdown = `A paragraph with *emphasis* and **strong importance**.

> A block quote with ~strikethrough~ and a URL: https://reactjs.org.

* Lists
* [ ] todo
* [x] done

A table:

| Branch  | Commit           |
| ------- | ---------------- |
| main    | 0123456789abcdef |
| staging | fedcba9876543210 |


# Hello 


`

export default class MarkdownTranslator extends React.Component {
  render () {
    return <ReactMarkdown children={markdown} remarkPlugins={[remarkGfm]} />
  }
}
