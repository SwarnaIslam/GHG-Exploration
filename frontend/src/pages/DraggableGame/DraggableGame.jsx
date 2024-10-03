import React, { useState } from 'react';
import './DraggableGame.css'; 
import { src } from '@/assets/constants'; // Update `src` to include categories
import { tickIcon,restart } from '@/assets/images';
import confetti from 'canvas-confetti';
import { useEffect } from 'react';



const DraggableGame = () => {


  const [droppedItems, setDroppedItems] = useState({
    human: [],
    natural: [],
  });
  const [showTick, setShowTick] = useState({
    human: false,
    natural: false,
  });

  const [gamefinish, setGameFinish] = useState(false);


  useEffect(() => {
    const score = droppedItems.human.length + droppedItems.natural.length;
    if (score === 10) {
      triggerConfetti();
      setGameFinish(true);
    }
  }, [droppedItems]);

  const triggerConfetti = () => {
    let duration = 2 * 1000;
    let animationEnd = Date.now() + duration;
    let defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

    function randomInRange(min, max) {
      return Math.random() * (max - min) + min;
    }

    let interval = setInterval(function() {
      let timeLeft = animationEnd - Date.now();

      if (timeLeft <= 0) {
        return clearInterval(interval);
      }

      let particleCount = 50 * (timeLeft / duration);
      confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }));
      confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }));
    }, 250);
  };


  const handleDragStart = (e) => {
    e.dataTransfer.setData('text/plain', e.target.id);
  };

  const handleDrop = (e, category) => {
    e.preventDefault();
    const draggedId = e.dataTransfer.getData('text/plain');
    const draggedItem = src.find((item) => item.id === draggedId);

    // Only allow items to be dropped in the correct category
    if (draggedItem && draggedItem.category === category) {
      setDroppedItems((prev) => ({
        ...prev,
        [category]: [...prev[category], draggedId],
      }));
      showTickWithTimeout(category);
    }
  };

  const showTickWithTimeout = (category) => {
    setShowTick((prev) => ({ ...prev, [category]: true }));
    setTimeout(() => {
      setShowTick((prev) => ({ ...prev, [category]: false }));
    }, 2000);
  };
 
  const handleDragOver = (e) => {
    e.preventDefault();
    e.target.classList.add('droppable-hover'); 
  };

  const handleRestart = () => {
    setGameFinish(false);
    setDroppedItems({
      human: [],
      natural: [],
    });
    setShowTick({
      human: false,
      natural: false,
    });
  };

  return (
    <div className="flex min-h-screen " style={{
      backgroundImage: 'url("bg.jpg")',
      backgroundPosition: "center",
      backgroundAttachment: "fixed",
      backgroundRepeat: "no-repeat",
      backgroundSize: "cover",
    }}>
    <div className="flex flex-col items-center w-full max-w-4xl mx-auto my-auto">
      <h1 className="text-[2.5rem] font-bold font-mono mt-[2rem]">Drag and Drop</h1>
      <p className="text-lg mt-2.5">Drag the items to the correct category, learn about human and natural green house sources!</p>
      <h1 className="text-2xl mt-[1rem] font-bold pr-[2rem]">Score: {droppedItems.human.length + droppedItems.natural.length}</h1>

      {/* Draggable items */}
      <section className="draggable-elements grid grid-cols-5 gap-4 w-full max-w-4xl p-4 mx-auto">
        {/* Render draggable items */}
        {src.map(({ id, imgURL, category }) =>
          (!droppedItems.human.includes(id) && !droppedItems.natural.includes(id)) ? (
            <img
              key={id}
              id={id}
              src={imgURL}
              alt={id}
              className="draggable"
              draggable
              onDragStart={handleDragStart}
              style={{ width: '124px', height: '128px', cursor: 'grab' }}
            />
          ) : null
        )}
      </section>

      <div className="flex flex-row xl:flex-col justify-evenly items-center">
        {/* Droppable area for human source */}
        <section className="droppable-elements flex justify-between items-center w-full max-w-4xl space-x-4">
          <div
            className={`droppable ${droppedItems.human.length ? 'dropped' : ''}`}
            onDrop={(e) => handleDrop(e, 'human')}
            onDragOver={handleDragOver}
          >
            <span className="text-xl font-bold">Human Source</span>
            {showTick.human && (
              <img src={tickIcon} alt="tick" className="tick-icon" />
            )}
          </div>

          {/* Droppable area for natural source */}
          <div
            className={`droppable ${droppedItems.natural.length ? 'dropped' : ''}`}
            onDrop={(e) => handleDrop(e, 'natural')}
            onDragOver={handleDragOver}
          >
            <span className="text-xl font-bold">Natural Source</span>
            {showTick.natural && (
              <img src={tickIcon} alt="tick" className="tick-icon" />
            )}
          </div>
        </section>
        <div className="relative mt-4 p-4">
          <img
            src={restart}
            alt="Restart Game"
            className="restart-icon cursor-pointer"
            onClick={handleRestart}
            height={50}
            width={50}
            title="Restart Game"
            

          />
          
        </div>

      </div>

      
      {gamefinish && (
          <div className="flex items-center justify-center w-full mt-4">
            <p className="text-2xl font-bold text-green-500">Congratulations! You have completed the game.</p>
          </div>
        )}

      
    </div>
    </div>
  );
};

export default DraggableGame;
