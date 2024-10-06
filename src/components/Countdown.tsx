import React, { useEffect, useState } from 'react';

interface CountdownProps {
  targetDate: string;
}

const Countdown: React.FC<CountdownProps> = ({ targetDate }) => {
  const calculateTimeLeft = () => {
    const difference = new Date(targetDate).getTime() - new Date().getTime();
    let timeLeft = {
      days: '0',
      hours: '0',
      minutes: '0',
      seconds: '0',
    };

    if (difference > 0) {
      timeLeft = {
        days: Math.floor(difference / (1000 * 60 * 60 * 24)).toString(),
        hours: Math.floor((difference / (1000 * 60 * 60)) % 24).toString(),
        minutes: Math.floor((difference / 1000 / 60) % 60).toString(),
        seconds: Math.floor((difference / 1000) % 60).toString(),
      };
    }

    return timeLeft;
  };

  const [timeLeft, setTimeLeft] = useState({
    days: '--',
    hours: '--',
    minutes: '--',
    seconds: '--',
  });

  useEffect(() => {
    setTimeLeft(calculateTimeLeft());

    const timer = setInterval(() => {
      setTimeLeft(calculateTimeLeft());
    }, 1000);

    return () => clearInterval(timer);
  }, [targetDate]);

  return (
    <div className="bg-gray-700 text-white font-sans">
      <div className="flex gap-2 text-2xl font-bold">
        <div className="flex flex-col items-center">
          <div className="text-4xl sm:text-2xl">{timeLeft.days}</div>
          <div className="text-xs uppercase">Days</div>
        </div>
        <div className="flex flex-col items-center">
          <div className="text-4xl sm:text-2xl">{timeLeft.hours}</div>
          <div className="text-xs uppercase">Hours</div>
        </div>
        <div className="flex flex-col items-center">
          <div className="text-4xl sm:text-2xl">{timeLeft.minutes}</div>
          <div className="text-xs uppercase">Minutes</div>
        </div>
        <div className="flex flex-col items-center">
          <div className="text-4xl sm:text-2xl">{timeLeft.seconds}</div>
          <div className="text-xs uppercase">Seconds</div>
        </div>
      </div>
    </div>
  );
};

export default Countdown;