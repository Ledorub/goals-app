import React from "react";

import FeatureList from "../feature-list/feature-list";
import FeatureItem from "../feature-item/feature-item";
import FeatureTitle from "../feature-title/feature-title";
import FeatureDescription from "../feature-description/feature-description";
import FeatureImg from "../feature-img/feature-img";

import "./home.css";


const FEATURES = [
    {
        name: 'Feature 1',
        description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        img: '/todo_list_1.svg'
    },
    {
        name: 'Feature 2',
        description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        img: '/todo_calendar_1.svg'
    },
    {
        name: 'Feature 3',
        description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        img: '/todo_list_2.svg'
    }
]


export default class Home extends React.Component {
    render() {
        return (
            <FeatureList className="feature-list">
                {FEATURES.map(({name, description, img}) => {
                    return (
                        <FeatureItem className="feature-list__item" key={name}>
                            <FeatureTitle className="feature-list__title">{name}</FeatureTitle>
                            <FeatureDescription className="feature-list__description">{description}</FeatureDescription>
                            {img && <FeatureImg className="feature-list__img" src={img} />}
                        </FeatureItem>
                    )
                })}
            </FeatureList>
        )
    }
}
