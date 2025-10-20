# Use a manylinux image to build portable Linux wheels
FROM quay.io/pypa/manylinux2014_x86_64

# Set up the environment to use Python 3.11
ENV PATH="/opt/python/cp311-cp311/bin:${PATH}"

# Install build dependencies, including auditwheel
RUN pip install --upgrade pip && pip install build cython auditwheel

# Set the working directory
WORKDIR /app

# The entrypoint will be a script that builds, repairs, and cleans up the wheel.
# This ensures only the correct 'manylinux' wheel is left for publishing.
ENTRYPOINT ["/bin/bash", "-c", "python3 -m build && auditwheel repair dist/*.whl -w dist/ && rm dist/*-linux_x86_64.whl"]
