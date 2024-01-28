ALL_GITLAB_VOLUMES=${1:-"./.gitlab_srv"}
PYTHON_PATH=${2:-"./venv/bin/python"}
TESTS_DIR=${3:-"."}
GITLAB_ROOT_PASSWORD_FILE_SAVE=${4:-"./.gitlab_root_password"}

# # # # # #
GITLAB_CONTAINERS=(
    gitlab/gitlab-ee:16.6.5-ee.0    gitlab_16.6
    gitlab/gitlab-ee:16.7.3-ee.0    gitlab_16.7
)
# # # # # #

for i in ${!GITLAB_CONTAINERS[*]}; do
    [[ $((i % 2)) == 1 ]] && continue  # skip if i - odd number

    DOCKER_CONTAINER=${GITLAB_CONTAINERS[$i]}
    DOCKER_NAME=${GITLAB_CONTAINERS[$((i + 1))]}

    echo "# # # Preparing for $DOCKER_NAME ... # # #"

    GITLAB_HOME="$ALL_GITLAB_VOLUMES/$DOCKER_NAME"
    ROOT_PERSONAL_ACCESS_TOKEN="test-access-token-$DOCKER_NAME"

    FIRST_TIME_LOADED=false
    if [ -z "$(docker ps -a -q --filter "name=$DOCKER_NAME")" ]; then
        docker run \
            --detach \
            --hostname localhost \
            --publish 443:443 \
            --publish 80:80 \
            --publish 22:22 \
            --name "$DOCKER_NAME" \
            --restart always \
            --volume "$GITLAB_HOME/config:/etc/gitlab" \
            --volume "$GITLAB_HOME/logs:/var/log/gitlab" \
            --volume "$GITLAB_HOME/data:/var/opt/gitlab" \
            --shm-size 256m \
            "$DOCKER_CONTAINER"
        FIRST_TIME_LOADED=true
    elif [ -z "$(docker ps -q --filter "name=$DOCKER_NAME")" ]; then
        docker start "$DOCKER_NAME"
    fi

    while [ -z "$(docker ps -q --filter "name=$DOCKER_NAME" --filter "health=healthy")" ];
    do
        sleep 1
    done

    docker ps -q --filter "name=$DOCKER_NAME" --filter "health=healthy"

    if $FIRST_TIME_LOADED; then
        echo "${DOCKER_NAME}: $(docker exec -it "$DOCKER_NAME" grep 'Password:' /etc/gitlab/initial_root_password | awk '{print $NF}')" >> "$GITLAB_ROOT_PASSWORD_FILE_SAVE"
    fi

    if [ "$(curl -o /dev/null -s -w "%{http_code}" --header "PRIVATE-TOKEN: $ROOT_PERSONAL_ACCESS_TOKEN" "http://localhost/api/v4/personal_access_tokens")" != "200" ]; then
        docker exec -it "$DOCKER_NAME" gitlab-rails runner \
            "token = User.find_by_username('root')
                         .personal_access_tokens
                         .find_or_create_by(
                             scopes: ['api', 'create_runner'],
                             name: 'Test token',
                             expires_at: 365.days.from_now,
                             revoked: false
                         );
            token.set_token('$ROOT_PERSONAL_ACCESS_TOKEN');
            token.save!"
    fi

    ROOT_PERSONAL_ACCESS_TOKEN=$ROOT_PERSONAL_ACCESS_TOKEN $PYTHON_PATH -m coverage run -m pytest "$TESTS_DIR"

    docker stop "$DOCKER_NAME"
done
