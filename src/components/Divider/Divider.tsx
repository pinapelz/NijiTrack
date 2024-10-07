interface DividerProps {
  text: string;
  description?: string;
}

const Divider = (props: DividerProps) => {
  return (
    <div className="flex flex-col items-center justify-center bg-black h-28 mx-6 sm:mx-12 md:mx-24 rounded-xl px-4 sm:px-12 md:px-72">
      <div className="px-2 mt-2 text-white text-2xl sm:text-3xl md:text-4xl font-extrabold">
        {props.text}
      </div>
      {props.description && (
        <div className="px-2 my-2 text-white text-sm sm:text-base md:text-lg font-medium">
          {props.description}
        </div>
      )}
    </div>
  );
};

export default Divider;