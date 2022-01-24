import React from 'react'
import getSelectedNode from './Canvas'
import '../styles/TextStyles.css'

export default function Properties() {
    return (
        // Return the parameters and input boxes for each action
        <div>
            <h2 className='HeadersDark'>Hello Properties!</h2>
            <div>getSelectedNode={getSelectedNode}</div>
        </div>
    )
}
