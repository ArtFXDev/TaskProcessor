import React from 'react'
import Properties from './Properties'
import ReactFlow, {
       Background, 
       MiniMap, 
       Controls,
      } from 'react-flow-renderer';

// Styles
import '../styles/PageStyles.css'
import '../styles/TextStyles.css'

const onElementClick = (event, element) => {
  console.log('click', element);
  <div className='NodeProperties'>
    <Properties />
  </div>
}

//Links
//  https://reactflow.dev/examples/update-node/
//  https://reactflow.dev/examples/edges/

const Canvas = () => {
  // Return the node graph system
  return(
    <div style={{height: '95vh'}}>
        <ReactFlow 
          elements={elements}
          onElementClick={onElementClick}
        >
          <Background 
            variant='dots'
            gap={25}
            size={1}/>
          <MiniMap
            nodeStrokeColor={(n) => {
              return '#000000';
            }}
            nodeColor={(n) => {
              return '#fff';
            }}/>
          <Controls/>
        </ReactFlow>
    </div>
  )
}
export default Canvas;

const elements = [
  {
    id: '1',
    type: 'input', // input node
    data: { label: 'Input Node' },
    position: { x: 250, y: 125 },
  },
  // default node
  {
    id: '2',
    // you can also pass a React component as a label
    data: { label: <div>Default Node</div> },
    position: { x: 250, y: 250 },
  },
  {
    id: '3',
    type: 'output', // output node
    data: { label: 'Output Node' },
    position: { x: 250, y: 375 },
  },
  // animated edge
  { id: 'e1-2', source: '1', target: '2', animated: true, type: 'smoothstep', label: 'E1-E2' },
  { id: 'e2-3', source: '2', target: '3', type: 'smoothstep' },
];
