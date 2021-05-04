FROM python:3.6

USER root

ENV WORKING_DIR /app/Relationship-Maintenance

COPY config /${WORKING_DIR}/config
COPY cron /${WORKING_DIR}/cron
COPY info_robot /${WORKING_DIR}/info_robot
COPY messenger /${WORKING_DIR}/messenger
COPY log.py /${WORKING_DIR}/log.py
COPY main.py /${WORKING_DIR}/main.py
COPY requirements.txt /${WORKING_DIR}/requirements.txt

RUN sh -c "echo 'Asia/Shanghai' > /etc/timezone" \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple\
    && pip install -r ./${WORKING_DIR}/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT cd ${WORKING_DIR}; python main.py;








