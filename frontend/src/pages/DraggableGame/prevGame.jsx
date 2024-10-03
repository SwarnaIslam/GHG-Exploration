import React, { useState } from 'react';
import './DraggableGame.css'; // Import your CSS here

const DraggableGame = () => {
  const [droppedItems, setDroppedItems] = useState({});

  const handleDragStart = (e) => {
    e.dataTransfer.setData('text/plain', e.target.id);
  };

  const handleDrop = (e, id) => {
    e.preventDefault();
    const draggedId = e.dataTransfer.getData('text/plain');
    if (draggedId === id) {
      setDroppedItems((prev) => ({ ...prev, [id]: draggedId }));
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const animals = [
    { id: 'cat', icon: 'fas fa-cat', color: '#ff6384' },
    { id: 'dog', icon: 'fas fa-dog', color: '#36a2eb' },
    { id: 'dove', icon: 'fas fa-dove', color: '#ffce56' },
    { id: 'fish', icon: 'fas fa-fish', color: '#9966ff' },
    { id: 'frog', icon: 'fas fa-frog', color: '#4bc0c0' },
  ];

  return (
    <div className="flex flex-col items-center">
      <section className="draggable-elements flex justify-center">
        {animals.map(({ id, icon, color }) => (
          <i
            key={id}
            id={id}
            className={`${icon} draggable`}
            draggable
            onDragStart={handleDragStart}
            style={{ color }}
          />
        ))}
      </section>
      <section className="droppable-elements flex flex-row justify-center">
        {animals.map(({ id }) => (
          <div
            key={id}
            className={`droppable ${droppedItems[id] ? 'dropped' : ''}`}
            onDrop={(e) => handleDrop(e, id)}
            onDragOver={handleDragOver}
          >
            <span>{id.charAt(0).toUpperCase() + id.slice(1)}</span>
            {droppedItems[id] && (
              <i className={`fas fa-${droppedItems[id]}`} />
            )}
          </div>
        ))}
      </section>
    </div>
  );
};

export default DraggableGame;
