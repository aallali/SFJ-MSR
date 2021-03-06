# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aallali <hi@allali.me>                     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/10/18 17:59:13 by aallali           #+#    #+#              #
#    Updated: 2021/10/18 18:00:55 by aallali          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=7080, reload=True)
