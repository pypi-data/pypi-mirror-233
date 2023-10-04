import jax
import jax.numpy as jnp
import time

if __name__ == '__main__':
    # Simple function that we'll JIT compile
    def slow_function(x):
        return jnp.dot(x, x)


    # JIT compile the function
    jit_slow_function = jax.jit(slow_function)


    def measure_execution_time(func, shape):
        x = jnp.ones(shape)
        start_time = time.time()
        _ = func(x)
        dt = time.time() - start_time
        print(dt, shape)
        return dt


    # Measure time for two different shapes
    shape_1 = (10000,)
    shape_2 = (20000,)

    # First call with shape_1
    time_1_first_call = measure_execution_time(jit_slow_function, shape_1)

    # First call with shape_2
    time_2_first_call = measure_execution_time(jit_slow_function, shape_2)

    # Second call with shape_1
    time_1_second_call = measure_execution_time(jit_slow_function, shape_1)

    assert time_1_first_call > time_1_second_call, "Caching not effective for shape_1!"
    assert time_1_first_call > time_2_first_call, "Expected first call with different shapes to have similar times!"

    print(f"First call with shape {shape_1}: {time_1_first_call:.6f} seconds")
    print(f"First call with shape {shape_2}: {time_2_first_call:.6f} seconds")
    print(f"Second call with shape {shape_1}: {time_1_second_call:.6f} seconds")
